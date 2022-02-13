extends Control
class_name Inventory_control
"""
Controls the inventory, like the move of items and the organization of them
"""

var item_focus = null

var open_crate = null

var slot_focus setget set_slot_focus,get_slot_focus

onready var inventory_keeper = get_node("Inventory keeper")

func _ready():
	set_process(false)
	
	inventory_keeper.load_inventory()
	
	sync_bar()
	$"Inventory bar".update_item_hand()

func _exit_tree():
	inventory_keeper.save_inventory()
	
	
func _process(_delta):
	if item_focus:
		item_focus.rect_position=get_local_mouse_position()-(item_focus.rect_size/2)
	

func click_item(slot):
	get_tree().set_input_as_handled()
#	var inventory = $Inventory
	if item_focus:
		if slot.get_child_count() != 0:
			var item_image = slot.get_child(0)
			var aux_item_image = item_image
			# Sacar de inv 
			slot.remove_child(aux_item_image)
			add_child(aux_item_image)
			
			# Meter en inv
			item_image = item_focus
			
			item_focus = null
			remove_child(item_image)
			slot.add_child(item_image)
			item_image.rect_position = Vector2(0,0)
			item_image.rect_size = item_image.get_parent().rect_size
			
			# Arreglo de el del mouse
			item_focus=aux_item_image
			item_focus.rect_position = Vector2(0,0)
			item_focus.rect_size.x = get_viewport_rect().size.x*0.039
			item_focus.rect_size.y = get_viewport_rect().size.y*0.066
			
		else:
			# Meto en inv desde mouse
			var item_image = item_focus
			item_focus = null
			remove_child(item_image)
			slot.add_child(item_image)
			item_image.rect_position = Vector2(0,0)
			item_image.rect_size = item_image.get_parent().rect_size
			
			set_process(false)
	else:
		
		if Input.is_action_pressed("ui_shift"):
			if slot.get_child_count() != 0:
				if open_crate:
					var item_image = slot.get_child(0)
					var reminer 
					if "Crate" in slot.get_parent().name:
						reminer = add_item(item_image.item_name,item_image.amount)
					else:
						reminer = open_crate.inventory.add_item(item_image.item_name,item_image.amount)
					if reminer == 0:
						item_image.free()
					else:
						if reminer != item_image.amount:
							item_image.amount -= reminer
		else:
			# Meto en mouse desde inv
			if slot.get_child_count() != 0:
				
				set_process(true)
				var item_image = slot.get_child(0)
				slot.remove_child(item_image)
				add_child(item_image)
				item_focus=item_image
				item_focus.rect_position = Vector2(0,0)
				item_focus.rect_size.x = get_viewport_rect().size.x*0.039
				item_focus.rect_size.y = get_viewport_rect().size.y*0.066
			
func _unhandled_input(_event):
	if item_focus:
#		if item_focus.item_name in global_var.POSIBLE_FURNITURE:
#			get_tree().get_nodes_in_group("Chunk_control")[0].construct_mode()
#			if Input.is_action_just_pressed("ui_left_click"):
#
#				get_tree().get_nodes_in_group("inventory")[0].remove_amount(item_focus,1)
#				get_tree().get_nodes_in_group("Chunk_control")[0].construct()
#
		if Input.is_action_just_pressed("ui_right_click"):
				drop_item()
				
func open_inv():
	$Inventory.open_inv()
	
	
func close_inv():
	$Inventory.close_inv()
	
	
func drop_item():
	
	if item_focus:
		var _position = get_tree().get_nodes_in_group("player")[0].position
		global.spawn_item(_position,item_focus.item_name,item_focus.amount)
		item_focus.queue_free()
		item_focus = null


func add_item(item_name, amount=1):
	var inventory = $Inventory
	# Busca si ya existe el item y lo stackea
	for slot in inventory.slots.values():
		if slot.get_child_count() != 0:
			var item_image = slot.get_child(0)
			if item_name == item_image.item_name:
				if item_image.amount+amount <= global_var.ITEM_STACK_LIMIT:
					item_image.amount+=amount
					sync_bar()
					return 0
				# Cuando se supera el stack limit
				else:
					if item_image.amount == global_var.ITEM_STACK_LIMIT:
						# Busca otro
						continue
					else:
						var fit = global_var.ITEM_STACK_LIMIT-item_image.amount
						
						item_image.amount+=fit
						amount-=fit
	
	# Busca un hueco para el nuevo item
	for slot in inventory.slots.values():
		if slot.get_child_count() == 0:
			var item_image = preload("res://prefabs/entity/item/Item image.tscn").instance()
			item_image.initialize(item_name,amount)

			slot.add_child(item_image)
			sync_bar()
			return 0
			
	return amount
			
func get_item(item_name):
	var inventory = $Inventory
	for slot in inventory.slots.values():
		if slot.get_child_count() != 0:
			if item_name == slot.get_child(0).item_name:
				return slot.get_child(0)
	
	return null
	
func remove_amount(item_image,amount):
	var inventory = $Inventory
	var inventory_bar = $"Inventory bar"

	if item_image.amount - amount <=0:
		item_image.free()
	else:
		item_image.amount-=amount
		
	#Busca en el inv
	var n_slot = inventory.search(item_image)
	
	if n_slot in [1,2,3,4,5,6,7,8]:
		sync_bar_slot(n_slot)
		return
		
	#Busca en la barra
	n_slot = inventory_bar.search(item_image)
	
	if n_slot:
		sync_inventory()
	
func sync_bar():
	var inventory_bar = $"Inventory bar"
	
	inventory_bar.clear()
	
	for slot_key in inventory_bar.slots.keys():
		sync_bar_slot(slot_key)
	
func sync_bar_slot(n_slot):
	var inventory = $Inventory
	var inventory_bar = $"Inventory bar"
	if n_slot:
		var slot = inventory.slots[n_slot]
		if slot.get_child_count() !=0:
			var item_image = slot.get_child(0)
			
			for child in inventory_bar.slots[n_slot].get_children():
				child.queue_free()
			
			var bar_item_image = preload("res://prefabs/entity/item/Item image.tscn").instance()
			bar_item_image.initialize(item_image.item_name,item_image.amount)
			inventory_bar.slots[n_slot].add_child(bar_item_image)

func sync_inventory():
	var inventory = $Inventory
	var inventory_bar = $"Inventory bar"
	
	for slot_key in inventory_bar.slots.keys():
		for child in inventory.slots[slot_key].get_children():
			child.queue_free()
			
		var slot = inventory_bar.slots[slot_key]
		if slot.get_child_count() !=0:
			var item_image = inventory_bar.slots[slot_key].get_child(0)
			
			var inv_item_image = preload("res://prefabs/entity/item/Item image.tscn").instance()
			inv_item_image.initialize(item_image.item_name,item_image.amount)
			inventory.slots[slot_key].add_child(inv_item_image)

func set_slot_focus(newFocus):
	$"Inventory bar".slot_focus = newFocus
	
func get_slot_focus():
	return $"Inventory bar".slot_focus
	
