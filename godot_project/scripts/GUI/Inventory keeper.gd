extends Node
class_name Inventory_keeper
"""
Saves inventory content and load it
"""

var directory_path = "res://save/inventory/"
var file_name = "inventory.save"

onready var inventory = get_node("../Inventory")

func save_inventory() -> void:
	var slot_dict = inventory.slots
	
	var file : = File.new()
	var directory : = Directory.new()
	
	var _err = directory.make_dir_recursive(directory_path)
	
	_err = file.open(directory_path+file_name,File.WRITE)
	
	var inv_dict = {}
	for slot_key in slot_dict.keys():
		var slot = slot_dict[slot_key]
		inv_dict[slot_key]={}
		if slot.get_child_count() !=0:
			var item_image = slot.get_child(0)
			inv_dict[slot_key]["item_name"]=item_image.item_name
			inv_dict[slot_key]["amount"]=item_image.amount
	
	file.store_line(to_json(inv_dict))
	
	file.close()
	
func load_inventory() -> void:
	
	inventory.clear_inventory()
	
	var file : = File.new()
	
	if file.file_exists(directory_path + file_name):
		var _err = file.open(directory_path + file_name,File.READ)
		
		var text = file.get_as_text()
		
		var inv_dict = parse_json(text)
		
		for slot_key in inv_dict.keys():
			if len(inv_dict[slot_key]) > 0:
				var item_image = preload("res://prefabs/entity/item/Item image.tscn").instance()
				item_image.initialize(inv_dict[slot_key]["item_name"],inv_dict[slot_key]["amount"])
				inventory.slots[int(slot_key)].add_child(item_image)
		
	file.close()
