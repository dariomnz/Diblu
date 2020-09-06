extends Item_hand


var player_to_attack = null

var can_attack

func _ready():
	set_process(false)
	set_process_unhandled_input(false)
	item_name = "iron_sword"
	var item_image_path = "res://assets/entity/item/item_hand/"+item_name+".png"
	var new_item_image = load(item_image_path)
	
	item_sprite.texture = new_item_image
	actionPlayer.play("setup")
	
	
#	set_current_rotation_degrees(randi()%360)
#@no_auto_basecall
func _physics_process(_delta):
	var direction = global_position.direction_to(get_tree().get_nodes_in_group("player")[0].global_position)
	var degrees = rad2deg( direction.angle())
	
	set_current_rotation_degrees(degrees)
	
	if player_to_attack and can_attack:
		action(1)
		can_attack = false
		$Attack_delay.start()

func _on_Trigger_attack_body_entered(body):
	if body in get_tree().get_nodes_in_group("player"):
		player_to_attack = body
		$Attack_delay.start()


func _on_Trigger_attack_body_exited(body):
	if body in get_tree().get_nodes_in_group("player"):
		player_to_attack = null
		can_attack = false
		$Attack_delay.stop()

func _on_HitBox_area_entered(area):
	if player.has_method("_on_HitBox_area_entered"):
		player._on_HitBox_area_entered(area)


func _on_Attack_delay_timeout():
	can_attack = true
