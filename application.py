from flask import Flask, render_template
from NamedAtomicLock import NamedAtomicLock
from fortune import fortune
from nms import frameinate

import cowsay

application = app = Flask(__name__)
frames_lock = NamedAtomicLock('wsgi-lock')

frames = []
frame_ptr = 0
@application.route('/frames')
def get_frame() -> str:
    global frames
    global frame_ptr

    frame = ''
    status = -1
    if frames_lock.acquire():
        print("frames (inside get_frame)=", len(frames))
        if len(frames) == 0:
            status = 2
        elif frame_ptr < len(frames):
            frame = frames[frame_ptr]
            frame_ptr += 1
        elif frame_ptr == len(frames):
            frame = frames[-1]
            status = 1
        print('get', frame_ptr, len(frames), status)

        frames_lock.release()
    return {'frame': frame, 'status': status}

@application.route('/')
def load() -> str:
    global frames
    global frame_ptr

    if frames_lock.acquire():
        text = cowsay.get_output_string('cow', fortune())
        frames = frameinate(text)
        frame_ptr = 0

        print('frames =', len(frames))
        frames_lock.release()
    return render_template('index.html')

if __name__ == "__main__":
    application.run()
