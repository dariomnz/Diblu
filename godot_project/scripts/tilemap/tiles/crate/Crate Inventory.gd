extends Control

onready var myTween : = $Tween

var inv_size = Vector2(200,200)

onready var slots = {
	1:get_node("Slot1"),
	2:get_node("Slot2"),
	3:get_node("Slot3"),
	4:get_node("Slot4"),
	5:get_node("Slot5"),
	6:get_node("Slot6"),
	7:get_node("Slot7"),
	8:get_node("Slot8"),
	9:get_node("Slot9"),
	10:get_node("Slot10"),
	11:get_node("Slot11"),
	12:get_node("Slot12"),
	13:get_node("Slot13"),
	14:get_node("Slot14"),
	15:get_node("Slot15"),
	16:get_node("Slot16"),
	17:get_node("Slot17"),
	18:get_node("Slot18"),
	19:get_node("Slot19"),
	20:get_node("Slot20"),
}

var is_destroy = false

func _ready():
	
	
	_update_size(Vector2(0,0))
	
	visible = true
	for slot in slots.values():
		slot.connect("clicked",get_tree().get_nodes_in_group("inventory")[0],"click_item")
	
	
	load_inv()

func open_inv():
	myTween.interpolate_method(self,"_update_size",Vector2(0,0),inv_size,0.2)
	myTween.start()
	
func close_inv():
	myTween.interpolate_method(self,"_update_size",inv_size,Vector2(0,0),0.2)
	myTween.start()
	
func _update_size(newSize):
	margin_left = -newSize.x
	margin_top = -newSize.y*2
	
	margin_right = newSize.x
	
	
func add_item(item_name, amount=1):
	# Busca si ya existe el item y lo stackea
	for slot in slots.values():
		if slot.get_child_count() != 0:
			var item_image = slot.get_child(0)
			if item_name == item_image.item_name:
				if item_image.amount+amount <= global_var.ITEM_STACK_LIMIT:
					item_image.amount+=amount
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
	for slot in slots.values():
		if slot.get_child_count() == 0:
#			var item_image = Item_image.new(item_name,amount)
			var item_image = preload("res://prefabs/entity/item/Item image.tscn").instance()
			item_image.initialize(item_name,amount)
#			item_image.item_name=item_name
#			item_image.amount=amount
			slot.add_child(item_image)
			return 0
			
	return amount
	
func _exit_tree():
	if not is_destroy:
		save_inv()


var directory_path = "res://save/chunk/crate/"
onready var file_name = get_parent().get_parent().id+".save"

func save_inv():
	var file : = File.new()
	var directory : = Directory.new()
	
	var _err = directory.make_dir_recursive(directory_path)
	
	_err = file.open(directory_path+file_name,File.WRITE)
	
	var inv_dict = {}
	for slot_key in slots.keys():
		var slot = slots[slot_key]
		inv_dict[slot_key]={}
		if slot.get_child_count() !=0:
			var item_image = slot.get_child(0)
			inv_dict[slot_key]["item_name"]=item_image.item_name
			inv_dict[slot_key]["amount"]=item_image.amount
	
	file.store_line(to_json(inv_dict))
	
	file.close()
	
func load_inv():
	
	
	var file : = File.new()
	
	if file.file_exists(directory_path + file_name):
		var _err = file.open(directory_path + file_name,File.READ)
		
		var text = file.get_as_text()
		
		var inv_dict = parse_json(text)
		
		for slot_key in inv_dict.keys():
			if len(inv_dict[slot_key]) > 0:
				var item_image = preload("res://prefabs/entity/item/Item image.tscn").instance()
				item_image.initialize(inv_dict[slot_key]["item_name"],inv_dict[slot_key]["amount"])

				slots[int(slot_key)].add_child(item_image)
		
	file.close()
	
func destroy():
	var directory : = Directory.new()
	
	var _err = directory.remove(directory_path + file_name)
	
	is_destroy = true
