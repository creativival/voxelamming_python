from voxelamming import Voxelamming

room_name = "1000"
voxelamming = Voxelamming(room_name)

voxelamming.set_box_size(0.5)
voxelamming.set_build_interval(0.01)
voxelamming.transform(0, 0, 0, pitch=0, yaw=0, roll=0)
voxelamming.animate(0, 0, 10, pitch=0, yaw=30, roll=0, scale=2, interval= 10)

for i in range(100):
  voxelamming.create_box(-1, i, 0, r=0, g=1, b=1)
  voxelamming.create_box(0, i, 0, r=1, g=0, b=0)
  voxelamming.create_box(1, i, 0, r=1, g=1, b=0)
  voxelamming.create_box(2, i, 0, r=0, g=1, b=1)

for i in range(50):
  voxelamming.remove_box(0, i * 2 + 1, 0)
  voxelamming.remove_box(1, i * 2, 0)

voxelamming.send_data('main')
