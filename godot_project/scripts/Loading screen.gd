extends Control


var new_scene_path = "res://scenes/Dungeon.tscn"
var loader : ResourceInteractiveLoader
var scene_instance

var actual_label_idx = 0
var label_list = ["Loading...","Loading..","Loading.","Loading","Loading","Loading.","Loading..","Loading..."]
#var num_rooms : int = 0
#var actual_num_rooms : int = 0
func _ready():
	$Loading_bar.value = 0
	
	loader = ResourceLoader.load_interactive(new_scene_path)
	
func _process(_delta):
	generate_dungeon()
		

func generate_dungeon():
	"""Return the percentage of the process"""
	if loader:
		var err = loader.poll()
		
		if err == ERR_FILE_EOF:
			var resource = loader.get_resource()
			loader = null
			scene_instance = resource.instance()
#		elif err == OK:
		if loader:
			change_bar(loader.get_stage()*1.0/loader.get_stage_count()* 100 *0.2)
			
	else:
		var _err = scene_instance.get_node("Dungeon").connect("upgrade_loading",self,"update_percentage")
#		num_rooms = scene_instance.get_node("Dungeon").num_rooms
		get_tree().root.add_child(scene_instance)
		
		set_process(false)
#		queue_free()
#	return 1.0

func update_percentage(newpercentage):
	change_bar(newpercentage * 100 * 0.8 + 100*0.2)
	
	if $Loading_bar.value == 100:
		start_transition()

func change_bar(newValue):
	$Loading_bar.value = newValue
	actual_label_idx = (actual_label_idx + 1) % len(label_list)
	$Label.text = label_list[actual_label_idx]
	
func start_transition():
	$Tween.interpolate_property(get_parent(),"modulate",null,Color(1.0,1.0,1.0,0),1)
	$Tween.start()
	yield($Tween,"tween_all_completed")
	get_parent().get_parent().queue_free()
