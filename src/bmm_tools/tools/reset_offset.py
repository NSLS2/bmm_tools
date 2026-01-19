def reset_offset(motor=None, newpos=0):
    current_offset  = motor.user_offset.get()
    current_position = motor.position
    new_offset = -1 * current_position + current_offset + newpos
    motor.user_offset.put(new_offset)
