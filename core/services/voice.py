from dataclasses import dataclass
import struct
from typing import Protocol

from core.services.orchestrator import JarvisOrchestrator


class SpeechToText(Protocol):
    def transcribe(self, audio: bytes) -> str:
        ...


class TextToSpeech(Protocol):
    def synthesize(self, text: str) -> bytes:
        ...


class VoiceActivityDetector(Protocol):
    def is_speech(self, audio_frame: bytes) -> bool:
        ...


class EnergyVAD:
    """Small local VAD for signed 16-bit PCM mono frames."""

    def __init__(self, threshold: int = 500) -> None:
        if threshold < 0:
            raise ValueError('VAD threshold cannot be negative.')
        self.threshold = threshold

    def is_speech(self, audio_frame: bytes) -> bool:
        if not audio_frame or len(audio_frame) % 2:
            raise ValueError('Audio frame must contain 16-bit PCM samples.')
        samples = struct.unpack(f'<{len(audio_frame) // 2}h', audio_frame)
        average_energy = sum(abs(sample) for sample in samples) / len(samples)
        return average_energy >= self.threshold


@dataclass(frozen=True)
class VoiceResult:
    transcript: str
    answer: str
    audio: bytes
    conversation_id: int


class VoicePipeline:
    def __init__(
        self,
        transcriber: SpeechToText,
        synthesizer: TextToSpeech,
        orchestrator: JarvisOrchestrator | None = None,
    ) -> None:
        self.transcriber = transcriber
        self.synthesizer = synthesizer
        self.orchestrator = orchestrator or JarvisOrchestrator()

    def process(self, audio: bytes) -> VoiceResult:
        if not audio:
            raise ValueError('Audio input cannot be empty.')
        transcript = self.transcriber.transcribe(audio).strip()
        if not transcript:
            raise ValueError('Speech transcription cannot be empty.')
        response = self.orchestrator.respond(transcript)
        return VoiceResult(
            transcript=transcript,
            answer=response['answer'],
            audio=self.synthesizer.synthesize(response['answer']),
            conversation_id=response['conversation_id'],
        )


class Utf8SpeechToText:
    """Offline adapter used for development until Whisper is configured."""

    def transcribe(self, audio: bytes) -> str:
        return audio.decode('utf-8')


class Utf8TextToSpeech:
    """Offline adapter used for development until a TTS provider is configured."""

    def synthesize(self, text: str) -> bytes:
        return text.encode('utf-8')
