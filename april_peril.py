from vhb import lsg, hbtg

h = hbtg(video_name="hearth")
lsg_ = lsg((255,216,0), (249, 77, 4), (124, 224, 9), "resources/full_lung_wb.png", video_name="lung", anim_len=2.5)

# h.start(80)
# h.linear_change(10, 100)
# h.stop()


lsg_.start(initial_air=1.0)
#lsg_.breathe(25)
lsg_.linear_change(5, .25)
lsg_.stop()