# ffmpeg_installer.py
import os
import platform
import subprocess
import webbrowser
import tkinter.messagebox as msg

def ensure_ffmpeg():
    """
    Verifica se o ffmpeg está disponível. Se não estiver, tenta baixar ou orienta o usuário.
    """
    from pydub.utils import which

    system = platform.system()
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg",
                                "ffmpeg.exe" if system == "Windows" else "ffmpeg")

    # Prioridade 1: ffmpeg embutido
    if os.path.exists(ffmpeg_path):
        return ffmpeg_path

    # Prioridade 2: ffmpeg no PATH
    found = which("ffmpeg")
    if found:
        return found

    # Prioridade 3: solicitar instalação
    if system == "Windows":
        msg.showwarning(
            "FFmpeg não encontrado",
            "FFmpeg é necessário para funcionar. Clique em OK para baixar."
        )
        webbrowser.open("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
    else:
        msg.showwarning(
            "FFmpeg não encontrado",
            "FFmpeg é necessário. No macOS use: brew install ffmpeg"
        )

    return None
