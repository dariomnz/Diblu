extends Live_entity
class_name entity_Skeleton

var attack_damage = 15

func _ready():
	animationPlayer = $Skeleton_animation
	
	is_going_to_escape = false
	set_physics_process(false)

func generate_item_loot():
	if rand.randi()%100 >30:
		global.spawn_item(global_position,"bone")
	

		
func _on_HitBox_area_entered(area):
	if area.get_parent() in get_tree().get_nodes_in_group("player"):
		if area.has_method("hit"):
			area.hit(self)

func set_physics_process(newBool):
	.set_physics_process(newBool)
	$Item_hand.set_physics_process(newBool)
