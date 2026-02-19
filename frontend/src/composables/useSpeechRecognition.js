import { ref } from 'vue'

export function useSpeechRecognition() {
    const isRecording = ref(false)
    const isPaused = ref(false)
    const isSupported = ref(false)
    const transcript = ref('')
    const error = ref('')

    let recognition = null
    let finalTranscript = ''
    let savedTranscript = '' // 暂停时保存的内容

    // 检测浏览器支持
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition
    if (SpeechRecognition) {
        isSupported.value = true
    }

    function createRecognition() {
        const rec = new SpeechRecognition()
        rec.continuous = true
        rec.interimResults = true
        rec.lang = 'zh-CN'

        rec.onresult = (event) => {
            let interim = ''
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i]
                if (result.isFinal) {
                    finalTranscript += result[0].transcript
                } else {
                    interim += result[0].transcript
                }
            }
            transcript.value = savedTranscript + finalTranscript + interim
        }

        rec.onerror = (event) => {
            if (event.error === 'no-speech') return
            if (event.error === 'not-allowed') {
                error.value = '麦克风权限被拒绝，请在浏览器设置中允许麦克风访问'
                stop()
                return
            }
            if (event.error === 'network') return // 网络波动不中断
            error.value = `语音识别错误: ${event.error}`
        }

        rec.onend = () => {
            // 如果是正常录制状态（非暂停），说明自动结束了，重启以保持持续录制
            if (isRecording.value && !isPaused.value) {
                try {
                    rec.start()
                } catch (_) { }
            }
        }

        return rec
    }

    function start() {
        if (!isSupported.value) {
            error.value = '您的浏览器不支持语音识别，请使用 Chrome 或 Edge 浏览器'
            return
        }
        error.value = ''
        finalTranscript = ''
        savedTranscript = transcript.value // 追加到已有内容后面
        if (savedTranscript && !savedTranscript.endsWith(' ')) {
            savedTranscript += ' '
        }

        recognition = createRecognition()
        recognition.start()
        isRecording.value = true
        isPaused.value = false
    }

    function pause() {
        if (!isRecording.value || isPaused.value) return
        isPaused.value = true
        savedTranscript = transcript.value
        finalTranscript = ''
        recognition?.stop()
    }

    function resume() {
        if (!isRecording.value || !isPaused.value) return
        isPaused.value = false
        finalTranscript = ''
        recognition = createRecognition()
        recognition.start()
    }

    function stop() {
        isRecording.value = false
        isPaused.value = false
        recognition?.stop()
        recognition = null
        finalTranscript = ''
        savedTranscript = ''
    }

    function clear() {
        stop()
        transcript.value = ''
    }

    return {
        isRecording,
        isPaused,
        isSupported,
        transcript,
        error,
        start,
        pause,
        resume,
        stop,
        clear,
    }
}
