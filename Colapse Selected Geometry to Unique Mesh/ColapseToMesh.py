import bpy

def collapse_selected_geometry():
    obj = bpy.context.active_object
    if not obj:
        print("No active object selected.")
        return

    # Step 1: Check for Geometry Nodes
    for mod in obj.modifiers:
        if mod.type == 'NODES':
            node_group = mod.node_group
            if node_group:
                # Check if Realize Instances node exists
                realize_found = any(node.bl_idname == 'GeometryNodeRealizeInstances' for node in node_group.nodes)
                if not realize_found:
                    print("Inserting Realize Instances node...")
                    # Insert Realize Instances before Group Output
                    output_node = next((n for n in node_group.nodes if n.bl_idname == 'NodeGroupOutput'), None)
                    if output_node:
                        realize_node = node_group.nodes.new("GeometryNodeRealizeInstances")
                        realize_node.location = output_node.location
                        # Reconnect
                        for input in output_node.inputs:
                            if input.is_linked:
                                link = input.links[0]
                                from_socket = link.from_socket
                                node_group.links.remove(link)
                                node_group.links.new(from_socket, realize_node.inputs[0])
                                node_group.links.new(realize_node.outputs[0], input)
                                break
                else:
                    print("Realize Instances node already present.")

            # Apply the Geometry Nodes modifier
            print("Applying Geometry Nodes modifier...")
            bpy.ops.object.modifier_apply(modifier=mod.name)
            break

    # Step 2: Make Instances Real (e.g., for Collection Instances)
    print("Making instances real (if any)...")
    bpy.ops.object.duplicates_make_real()

    # Step 3: Ensure the mesh is unique (not linked to other objects)
    print("Making mesh data unique...")
    bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

    print("Done: Selected object is now a unique, non-instanced mesh.")

collapse_selected_geometry()
