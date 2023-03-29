
# Blender Tools

## Create Unreal Collision AABB

file:
  create_unreal_collision_aabb.py

    description:
  Create a wire axis-aligned box to bound selected objects.  The newly created object is named with the UBX_ prefix so it can be imported into
  Unreal as collision.  The new object is placed in its own collection with other collision objects (makes it easy to show/hide
  all collision).

    install:
  in Blender, Edit menu -> Preferences -> Install
  choose this py file
  then enable this python file in the list "Add Mesh: Create Unreal Collision AABB"

    typical usage:
  select objects to bound with a box, then shift+A to get the add menu, go to Mesh sub menu, then choose "Create Unreal Collision AABB"
  the created box will be located under a collection with the name "Collision_" + the name of the first selected object, the collection will be
    created if it doesn't exist
  all created boxes get the prefix "UBX_" so on import into Unreal they will be treated as collision
  if needed, it is safe to rotate the box after creation

    exporting:
  select all the cosmetic geometry and all the collision boxes
  choose to export fbx with the selected objects option checked



## Create Unreal Collision OBB

file:
  create_unreal_collision_obb.py

    description:
  Create a wire oriented box to bound selected objects.  The newly created object is named with the UBX_ prefix so it can be imported into
  Unreal as collision.  The new object is placed in its own collection with other collision objects (makes it easy to show/hide
  all collision).

    install:
  in Blender, Edit menu -> Preferences -> Install
  choose this py file
  then enable this python file in the list "Add Mesh: Create Unreal Collision OBB"

    typical usage:
  select the minimal number of objects to bound with a box, then shift+A to get the add menu, go to Mesh sub menu, then choose "Create Unreal Collision OBB"
  if the generated box doesn't bound the selection very well, try reducing the number of selected objects if possible (remove unneeded internal objects, just 
    select the objects on the boundaries of where the box needs to bound)
  the created box will be located under a collection with the name "Collision_" + the name of the first selected object, the collection will be
    created if it doesn't exist
  all created boxes get the prefix "UBX_" so on import into Unreal they will be treated as collision

    exporting:
  select all the cosmetic geometry and all the collision boxes
  choose to export fbx with the selected objects option checked

