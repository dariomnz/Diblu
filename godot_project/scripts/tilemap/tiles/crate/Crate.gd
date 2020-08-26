extends "res://scripts/tilemap/tiles/Furniture.gd"


onready var inventory : = $"Scale inv/Crate Inventory"


var is_inventory = false

func _hit(_hitter):
	if not is_inventory:
		$AnimationPlayer.play("hit")
		
	health -= 1
	$Regen_timer.start()
	
	if health == 0:
		destroy()

func destroy():
	.destroy()
	global.spawn_item(position,"crate")
	for slot in inventory.slots.values():
		if slot.get_child_count() != 0:
			var item_image = slot.get_child(0)
			global.spawn_item(position,item_image.item_name,item_image.amount)
	inventory.destroy()
	

func _on_Open_crate_pressed():
#	var inv_open_crate = get_tree().get_nodes_in_group("inventory control")[0].open_crate
		
	if is_inventory:
		$AnimationPlayer.play("close_inv")
		inventory.close_inv()
		
		get_tree().get_nodes_in_group("inventory")[0].open_crate = null
	else:
		$AnimationPlayer.play("open_inv")
		inventory.open_inv()
		var inv_open_crate = get_tree().get_nodes_in_group("inventory")[0].open_crate
	
		if inv_open_crate:
			inv_open_crate._on_Open_crate_pressed()
			
		get_tree().get_nodes_in_group("inventory")[0].open_crate = self
		
	is_inventory = !is_inventory



