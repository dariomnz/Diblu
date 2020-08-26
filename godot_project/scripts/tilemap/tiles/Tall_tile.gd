extends StaticBody2D

onready var myTween : Tween = $Tween
var sprite
var timer

var obj_inside = 0

var posible_tiles = {}

func parent_ready():
	var childrens = get_children()
	for child in childrens:
		if "sprite" in child.name:
			sprite = child
		if "Timer" in child.name:
			timer = child
	
	randomize()
	var num = randi()%len(posible_tiles)+1
	sprite.region_rect=Rect2(posible_tiles[num][0],posible_tiles[num][1],posible_tiles[num][2],posible_tiles[num][3])
	
	# Para ponerlo centrado top-left
	var adjustment = Vector2(sprite.region_rect.size.x/2,sprite.region_rect.size.y/2)
	
	if "Palm" in sprite.name:
		adjustment.y+=36
	else:
		adjustment.y+=15
		
	
	translate(adjustment)

func do_transparent():
	var _bool = myTween.interpolate_property(self,"modulate",Color(1.0,1.0,1.0,1.0),Color(1.0,1.0,1.0,0.5),0.25)
	_bool =myTween.start()
#	sprite.modulate.a=0.5
	
func do_opaque():
	var _bool =myTween.interpolate_property(self,"modulate",Color(1.0,1.0,1.0,0.5),Color(1.0,1.0,1.0,1.0),0.25)
	_bool =myTween.start()
#	sprite.modulate.a=1

# Cuando termina el timer
func _on_Timer_timeout():
	do_opaque()

# Cuando entra un body
func _on_area_leaves_body_entered(body):
	if body in get_tree().get_nodes_in_group("entity"):
		obj_inside+=1
		if timer.is_inside_tree():
			timer.stop()
			do_transparent()
		
# Cuando entra un area
func _on_area_leaves_area_entered(area):
	if area in get_tree().get_nodes_in_group("entity"):
		obj_inside+=1
		if timer.is_inside_tree():
			timer.stop()
			do_transparent()
			
			
# Cuando sale un body
func _on_area_leaves_body_exited(body):
	if body in get_tree().get_nodes_in_group("entity"):
		obj_inside-=1
		if obj_inside==0:
			if timer.is_inside_tree():
				timer.start()

# Cuando sale un area
func _on_area_leaves_area_exited(area):
	if area in get_tree().get_nodes_in_group("entity"):
		obj_inside-=1
		if obj_inside==0:
			if timer.is_inside_tree():
				timer.start()
