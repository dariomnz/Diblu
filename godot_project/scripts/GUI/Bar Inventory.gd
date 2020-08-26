extends Control

onready var slots = {
	1:get_node("Slot1"),
	2:get_node("Slot2"),
	3:get_node("Slot3"),
	4:get_node("Slot4"),
	5:get_node("Slot5"),
	6:get_node("Slot6"),
	7:get_node("Slot7"),
	8:get_node("Slot8"),
}

onready var slot_focus = slots[1] setget set_slot_focus

func _ready():
	for slot in slots.values():
		slot.connect("clicked",self,"click_item")
		
	upgrade_slot_size(slot_focus,3)
		
func _unhandled_input(_event):
	for slot_key in slots.keys():
		if Input.is_action_just_pressed("ui_"+str(slot_key)):
			set_slot_focus(slots[slot_key])
	
func set_slot_focus(newSlot_focus):
	
	var theme_slot_focus = preload("res://assets/GUI/focus_slot.tres")
	
	slot_focus.theme = null
	upgrade_slot_size(slot_focus,-3)
	
	slot_focus = newSlot_focus
	
	slot_focus.theme = theme_slot_focus
	upgrade_slot_size(slot_focus,3)
	
	update_item_hand()

func upgrade_slot_size(slot,upgrade_size):
	slot.margin_top-=upgrade_size
	slot.margin_bottom+=upgrade_size
	slot.margin_left-=upgrade_size
	slot.margin_right+=upgrade_size

func update_item_hand():
	if slot_focus.get_child_count() != 0:
		var item_image = slot_focus.get_child(0)
	
		get_tree().get_nodes_in_group("player")[0].update_item_hand(item_image)
		
	else:
		get_tree().get_nodes_in_group("player")[0].update_item_hand(null)

func click_item(slot):
	get_parent().click_item(slot)
	
	update_item_hand()
	get_parent().sync_inventory()

func clear():
	for slot in slots.values():
		for child in slot.get_children():
			child.queue_free()

func search(item_image):
	for slot_key in slots.keys():
		var slot = slots[slot_key]
		if slot.get_child_count() !=0:
			if item_image == slot.get_child(0):
				return slot_key
	return null
