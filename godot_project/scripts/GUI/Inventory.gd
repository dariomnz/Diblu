extends Control

onready var myTween : = $Tween

onready var slots : = {
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
}


func _ready():
	for slot in slots.values():
		slot.connect("clicked",self,"click_item")
	visible = true
	_update_size(Vector2(0,0))
	
	load_inventory()
	
	get_parent().sync_bar()
	
	get_node("../Inventory bar").update_item_hand()

func _exit_tree():
	save_inventory()

func open_inv():
	var screen_size = get_viewport_rect().size
	myTween.interpolate_method(self,"_update_size",Vector2(0,0),screen_size,0.2)
	myTween.start()
	
func close_inv():
	var screen_size = get_viewport_rect().size
	myTween.interpolate_method(self,"_update_size",screen_size,Vector2(0,0),0.2)
	myTween.start()

func _update_size(newSize):
	margin_left = -newSize.x/2
	margin_top = -newSize.y/2

func click_item(slot):
	get_parent().click_item(slot)
	
	get_parent().sync_bar()



func clear_inventory():
	for slot_key in slots.keys():
		for child in slots[slot_key].get_children():
			child.queue_free()

var directory_path = "res://save/inventory/"
var file_name = "inventory.save"

func save_inventory():
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
	
func load_inventory():
	
	clear_inventory()
	
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

func search(item_image):
	for slot_key in slots.keys():
		var slot = slots[slot_key]
		if slot.get_child_count() !=0:
			if item_image == slot.get_child(0):
				return slot_key
	return null

