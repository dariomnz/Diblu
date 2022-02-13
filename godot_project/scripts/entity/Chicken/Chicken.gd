extends Live_entity


func _ready():
	animationPlayer = $Chicken_animation

func generate_item_loot():
	if rand.randi()%100 <30:
		global.spawn_item(global_position,"golden_feather")
	else:
		global.spawn_item(global_position,"feather")
