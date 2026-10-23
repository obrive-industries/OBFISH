/**
 * IndexedDB Pending Upload Persistence (SEC-04 / DATA-02)
 *
 * Persists pending upload data (files & scenario hypothesis) in IndexedDB.
 * Eliminates the 5MB localStorage limit and avoids base64 encoding crashes
 * with large PDFs, DOCX, and documents.
 *
 * Database: 'obmind_store'
 * Object Store: 'pending_uploads'
 * Key: 'current_upload'
 */

import { reactive } from 'vue'

const DB_NAME = 'obmind_store'
const DB_VERSION = 1
const STORE_NAME = 'pending_uploads'
const RECORD_KEY = 'current_upload'

// In-memory reactive state for instant reactivity in Vue components
export const state = reactive({
  files: [],
  simulationRequirement: '',
  isPending: false
})

/**
 * Open IndexedDB instance with graceful fallback
 */
function openDB() {
  return new Promise((resolve, reject) => {
    if (typeof window === 'undefined' || !window.indexedDB) {
      return reject(new Error('IndexedDB is not supported in this environment'))
    }

    const request = window.indexedDB.open(DB_NAME, DB_VERSION)

    request.onupgradeneeded = (event) => {
      const db = event.target.result
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'id' })
      }
    }

    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error || new Error('Failed to open IndexedDB'))
  })
}

/**
 * Retrieve the pending upload record directly from IndexedDB
 */
async function getRecordFromIDB(key) {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readonly')
      const store = tx.objectStore(STORE_NAME)
      const req = store.get(key)
      req.onsuccess = () => resolve(req.result || null)
      req.onerror = () => reject(req.error)
      tx.onabort = () => reject(tx.error)
    })
  } catch (err) {
    console.warn('[pendingUpload] IndexedDB read fallback:', err.message)
    return null
  }
}

/**
 * Save record into IndexedDB
 */
async function saveRecordToIDB(record) {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite')
      const store = tx.objectStore(STORE_NAME)
      store.put(record)
      tx.oncomplete = () => resolve(true)
      tx.onerror = () => reject(tx.error)
      tx.onabort = () => reject(tx.error)
    })
  } catch (err) {
    console.warn('[pendingUpload] IndexedDB write fallback:', err.message)
    return false
  }
}

/**
 * Delete record from IndexedDB
 */
async function deleteRecordFromIDB(key) {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite')
      const store = tx.objectStore(STORE_NAME)
      store.delete(key)
      tx.oncomplete = () => resolve(true)
      tx.onerror = () => reject(tx.error)
      tx.onabort = () => reject(tx.error)
    })
  } catch (err) {
    console.warn('[pendingUpload] IndexedDB delete fallback:', err.message)
    return false
  }
}

/**
 * Save pending upload files and hypothesis prompt into IndexedDB
 * Accepts flexible parameters:
 *   - savePendingUpload({ files, simulationRequirement })
 *   - savePendingUpload(files, requirement)
 *   - savePendingUpload(file)
 *   - savePendingUpload(requirementString)
 *
 * @param {Array|Object|File|Blob|string} fileOrData
 * @param {string} [maybeRequirement]
 * @returns {Promise<{files: File[], simulationRequirement: string, isPending: boolean}>}
 */
export async function savePendingUpload(fileOrData, maybeRequirement = '') {
  let files = []
  let simulationRequirement = ''

  if (Array.isArray(fileOrData)) {
    files = fileOrData
    simulationRequirement = typeof maybeRequirement === 'string' ? maybeRequirement : ''
  } else if (typeof fileOrData === 'string') {
    simulationRequirement = fileOrData
    files = Array.isArray(maybeRequirement) ? maybeRequirement : []
  } else if (fileOrData && typeof fileOrData === 'object') {
    if (fileOrData instanceof Blob || (typeof File !== 'undefined' && fileOrData instanceof File)) {
      files = [fileOrData]
      simulationRequirement = typeof maybeRequirement === 'string' ? maybeRequirement : ''
    } else {
      files = fileOrData.files || (fileOrData.file ? [fileOrData.file] : [])
      simulationRequirement = fileOrData.simulationRequirement || fileOrData.requirement || fileOrData.prompt || ''
    }
  }

  // Update in-memory reactive state
  state.files = files
  state.simulationRequirement = simulationRequirement
  state.isPending = Boolean(files.length > 0 || simulationRequirement.trim())

  // Serialize file entries preserving metadata alongside blob
  const serializedFiles = files.map((f) => {
    return {
      blob: f,
      name: f.name || 'document',
      type: f.type || 'application/octet-stream',
      lastModified: f.lastModified || Date.now(),
      size: f.size || (f.blob ? f.blob.size : 0)
    }
  })

  // Persist to IndexedDB
  await saveRecordToIDB({
    id: RECORD_KEY,
    files: serializedFiles,
    simulationRequirement,
    updatedAt: Date.now()
  })

  return {
    files: state.files,
    simulationRequirement: state.simulationRequirement,
    isPending: state.isPending
  }
}

/**
 * Alias for backward compatibility with existing components
 */
export function setPendingUpload(files, requirement) {
  return savePendingUpload(files, requirement)
}

/**
 * Retrieve pending upload data from IndexedDB
 * Returns a Promise that resolves to { files, simulationRequirement, isPending }.
 * Also exposes synchronous getters on the returned promise for legacy synchronous callers.
 */
export function getPendingUpload() {
  const promise = (async () => {
    const record = await getRecordFromIDB(RECORD_KEY)
    if (record) {
      const reconstructedFiles = (record.files || []).map((item) => {
        if (typeof File !== 'undefined' && item.blob) {
          if (item.blob instanceof File) return item.blob
          return new File([item.blob], item.name || 'document', {
            type: item.type || 'application/octet-stream',
            lastModified: item.lastModified || Date.now()
          })
        }
        return item.blob || item
      })

      state.files = reconstructedFiles
      state.simulationRequirement = record.simulationRequirement || ''
      state.isPending = Boolean(
        state.files.length > 0 || state.simulationRequirement.trim()
      )
    }
    return {
      files: state.files,
      simulationRequirement: state.simulationRequirement,
      isPending: state.isPending
    }
  })()

  // Provide synchronous access bridge so synchronous calls (like if (pending.isPending)) work
  Object.defineProperties(promise, {
    files: {
      get: () => state.files,
      enumerable: true
    },
    simulationRequirement: {
      get: () => state.simulationRequirement,
      enumerable: true
    },
    isPending: {
      get: () => state.isPending,
      enumerable: true
    }
  })

  return promise
}

/**
 * Clear pending upload from both memory and IndexedDB
 */
export async function clearPendingUpload() {
  state.files = []
  state.simulationRequirement = ''
  state.isPending = false

  // Clear legacy localStorage cache key if present
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('obmind_pending_prompt')
    }
  } catch (e) {
    // Ignore localStorage access errors
  }

  await deleteRecordFromIDB(RECORD_KEY)
}

// Immediate asynchronous hydration on module import
if (typeof window !== 'undefined') {
  getPendingUpload().catch(() => {})
}

export default state
