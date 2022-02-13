extends Live_entity

var dino_colors = ["green","red","blue","yellow"]
var dino_color : String

func _ready():
	animationPlayer = $Dino_animation
	
	can_escape = false
	
	dino_color = dino_colors[randi()%len(dino_colors)]
	
	$Dino_sprite.texture = load("res://assets/entity/dino/"+dino_color+"_Dino.png")
	
func generate_item_loot():
	if rand.randi()%100 <30:
		global.spawn_item(global_position,dino_color+"_gem")
	else:
		global.spawn_item(global_position,"bone")
	
