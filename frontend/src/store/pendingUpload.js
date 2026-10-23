/**
 * 临时存储待上传的文件和需求
 * 用于首页点击启动引擎后立即跳转，在Process页面再进行API调用
 */
import { reactive } from 'vue'

const PROMPT_KEY = 'obmind_pending_prompt'

const state = reactive({
  files: [],
  simulationRequirement: localStorage.getItem(PROMPT_KEY) || '',
  isPending: Boolean(localStorage.getItem(PROMPT_KEY))
})

export function setPendingUpload(files, requirement) {
  state.files = files
  state.simulationRequirement = requirement
  state.isPending = true
  if (requirement) {
    try {
      localStorage.setItem(PROMPT_KEY, requirement)
    } catch (e) {
      console.warn('Failed to cache pending prompt in localStorage:', e)
    }
  }
}

export function getPendingUpload() {
  return {
    files: state.files,
    simulationRequirement: state.simulationRequirement,
    isPending: state.isPending
  }
}

export function clearPendingUpload() {
  state.files = []
  state.simulationRequirement = ''
  state.isPending = false
  try {
    localStorage.removeItem(PROMPT_KEY)
  } catch (e) {
    console.warn('Failed to clear pending prompt cache:', e)
  }
}

export default state
