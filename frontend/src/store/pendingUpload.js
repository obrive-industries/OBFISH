/**
 * Pending Upload Store
 * Re-exports the IndexedDB-backed implementation from utils/pendingUpload.js
 * for unified state management and backward compatibility across the app.
 */

export {
  state,
  savePendingUpload,
  setPendingUpload,
  getPendingUpload,
  clearPendingUpload,
  default
} from '../utils/pendingUpload.js'
