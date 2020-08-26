extends Item_hand

func _ready():
	var item_image_path = "res://assets/entity/item/item_hand/"+item_name+".png"
	var new_item_image = load(item_image_path)
	
	item_sprite.texture = new_item_image
	
	actionPlayer.play("setup")


func _on_HitBox_area_entered(area):
	player._on_HitBox_area_entered(area)
