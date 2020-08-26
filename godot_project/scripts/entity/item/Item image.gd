extends MarginContainer

class_name Item_image

var item_name : String setget set_item_name

var item_image 

var amount = 1 setget set_amount

func initialize(_item_name, _amount=1):
	set_item_name(_item_name)
	set_amount(_amount)
	
#func _ready():
#	set_item_name("green_apple")
#	set_amount(300)
#	pass # Replace with function body.

func set_item_name(newName : String):
	item_name = newName
	
	var path = "res://assets/entity/item/"+item_name+".png"
	item_image = load(path)
	
	$Image.texture = item_image
	
	
func set_amount(newAmount):
	amount = newAmount
	$Number.text = str(newAmount)

