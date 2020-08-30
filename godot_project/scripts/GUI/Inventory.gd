extends Control
class_name Inventory
"""
Control the inventory, open and close the visual
"""

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
	
	get_node("../Inventory bar").update_item_hand()

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

func search(item_image):
	for slot_key in slots.keys():
		var slot = slots[slot_key]
		if slot.get_child_count() !=0:
			if item_image == slot.get_child(0):
				return slot_key
	return null
