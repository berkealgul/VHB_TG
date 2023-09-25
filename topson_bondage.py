from vhb import lsg, hbtg


lsg_ = lsg((72,255,0), (249, 77, 4), (255,216,0), "resources/full_lung_og.png", video_name="lung", anim_len=2.5)

lsg_.start(initial_air=1.0)
lsg_.linear_change(43, .60)
lsg_.linear_change(38, .0) # her air depletes
lsg_.constant_change(7) # holds
lsg_.linear_change(3, -.15) # initial inhale
lsg_.constant_change(52) 
lsg_.linear_change(3, -.30) # burst inhale
lsg_.linear_change(23, -2.0) # breathes water inhale # holds
lsg_.constant_change(10) # ex
lsg_.stop()


# h = hbtg(video_name="hearth")
# h.start(80)
# h.linear_change(10, 100)
# h.stop()