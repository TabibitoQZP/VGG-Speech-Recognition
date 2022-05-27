import pyaudio
import wave
import threading
import keyboard
import os

recording = True
record_continue = True

def fuck():
    global recording, record_continue
    while record_continue:
        keyboard.wait('d')
        recording = False


def record_audio(WAVE_OUTPUT_FILENAME):
    global recording
    FORMAT = pyaudio.paInt32
    CHANNELS = 1
    RATE = 8000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    frames = []
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print('press "s" to record')
    keyboard.wait('s')
    recording = True
    print("recording..., press 'd' to finish")

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def init_path(root_path):
    if os.path.isdir(root_path):
        return 0
    else:
        os.mkdir(root_path)
        for i in range(0, 10):
            tmp = os.path.join(root_path, '0' + str(i))
            os.mkdir(tmp)
            tmp = os.path.join(root_path, '1' + str(i))
            os.mkdir(tmp)


def write_to_path(root_path, sid):
    global record_continue
    dir_path = []
    for i in range(0, 10):
        dir_path.append('0' + str(i))
        dir_path.append('1' + str(i))
    dir_path.sort()
    for i in dir_path:
        print(i + ' is recording!')
        keep = input('do you want to record i?')
        if keep == 'n':
            continue
        j = 0
        while j < 20:
            if j < 10:
                file_name = sid + '_' + i + '_0' + str(j) + '.wav'
            else:
                file_name = sid + '_' + i + '_' + str(j) + '.wav'
            print(i, j, 'is recording!')
            full_file_name = os.path.join(root_path, i, file_name)
            record_audio(full_file_name)
            j += 1
    record_continue = False


def change_format(root_path, original_format, dest_format):
    root_contain = os.listdir(root_path)
    for i in root_contain:
        tmp = os.path.join(root_path, i)
        if os.path.isdir(tmp):
            change_format(tmp, original_format, dest_format)
        else:
            file_path, full_file_name = os.path.split(tmp)
            file_name, ext = os.path.splitext(full_file_name)
            if ext == original_format:
                os.rename(tmp, os.path.join(file_path, file_name + dest_format))


if __name__ == '__main__':
    th = threading.Thread(target=fuck)
    th.start()
    init_path('./data')
    write_to_path('./data', '20307130150')
    change_format('./data', '.wav', '.dat')
