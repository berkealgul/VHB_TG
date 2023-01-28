from vhb import lsg, hbtg


lsg_ = lsg((72,255,0), (249, 77, 4), (255,216,0), "resources/full_lung_og.png", video_name="lung", anim_len=2.5)

lsg_.start(initial_air=1.0)
lsg_.breathe(25)
lsg_.linear_change(15, .65)
lsg_.linear_change(5, 1.0)
lsg_.breathe(40)
lsg_.linear_change(5, .90)
lsg_.linear_change(5, 1.0) # 1.35
lsg_.breathe(15)
lsg_.linear_change(68, .45) # 2.58
lsg_.linear_change(7, 1.0) # 2.58
lsg_.breathe(15) # 3.20
lsg_.linear_change(87, .35) # 4.47
lsg_.linear_change(28, .15) # 6.15
lsg_.linear_change(1, .20) # 6.16
lsg_.linear_change(24, 0.0) # 6.40
lsg_.constant_change(35)
lsg_.linear_change(20, -.25) # 7.15
lsg_.linear_change(5, -.40) 
lsg_.linear_change(40, -.80) 
lsg_.constant_change(60)
lsg_.stop()


# h = hbtg(video_name="hearth")
# h.start(80)
# h.linear_change(10, 100)
# h.stop()