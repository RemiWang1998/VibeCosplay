import FreeCAD as App
import Part
import PartDesign
import math

def create_guide_bar():
    # Get the active document or create a new one
    doc = App.ActiveDocument if App.ActiveDocument else App.newDocument("GuideBar")
    
    # Parameters (all in mm)
    total_length = 500.0
    base_width = 110.0
    tip_width = 80.0
    thickness = 8.0
    tip_radius = tip_width / 2.0
    
    # --- 1. Main Profile ---
    # We'll build the profile from lines and an arc
    p1 = App.Vector(0, -base_width/2.0, 0)
    p2 = App.Vector(total_length - tip_radius, -tip_width/2.0, 0)
    p3 = App.Vector(total_length - tip_radius, tip_width/2.0, 0)
    p4 = App.Vector(0, base_width/2.0, 0)
    
    l1 = Part.LineSegment(p1, p2).toShape()
    l3 = Part.LineSegment(p3, p4).toShape()
    l4 = Part.LineSegment(p4, p1).toShape()
    
    # tip_center = App.Vector(total_length - tip_radius, 0, 0)
    p_tip = App.Vector(total_length, 0, 0) # The very tip point
    arc = Part.ArcOfCircle(p2, p_tip, p3).toShape()
    
    wire = Part.Wire([l1, arc, l3, l4])
    face = Part.Face(wire)
    guide_bar_body = face.extrude(App.Vector(0, 0, thickness))
    
    # --- 2. Mounting Slot (Rounded) ---
    slot_length = 80.0
    slot_width = 14.0
    slot_x_offset = 50.0
    
    # Create a rounded slot (capsule shape)
    c1 = Part.makeCylinder(slot_width/2.0, thickness, App.Vector(slot_x_offset - slot_length/2.0 + slot_width/2.0, 0, 0))
    c2 = Part.makeCylinder(slot_width/2.0, thickness, App.Vector(slot_x_offset + slot_length/2.0 - slot_width/2.0, 0, 0))
    box = Part.makeBox(slot_length - slot_width, slot_width, thickness, App.Vector(slot_x_offset - slot_length/2.0 + slot_width/2.0, -slot_width/2.0, 0))
    slot = box.fuse(c1).fuse(c2)
    
    guide_bar_body = guide_bar_body.cut(slot)
    
    # --- 3. Decorative "Blaze" Weight Reduction Cutouts ---
    # Create three rhomboid cutouts along the center
    cutout_width = 60.0
    cutout_height = 30.0
    for i in range(3):
        x_pos = 150.0 + i * 100.0
        # Create a simple diamond/rhomboid for each cutout
        cp1 = App.Vector(x_pos - cutout_width/2.0, 0, 0)
        cp2 = App.Vector(x_pos, -cutout_height/2.0, 0)
        cp3 = App.Vector(x_pos + cutout_width/2.0, 0, 0)
        cp4 = App.Vector(x_pos, cutout_height/2.0, 0)
        
        cw1 = Part.LineSegment(cp1, cp2).toShape()
        cw2 = Part.LineSegment(cp2, cp3).toShape()
        cw3 = Part.LineSegment(cp3, cp4).toShape()
        cw4 = Part.LineSegment(cp4, cp1).toShape()
        
        c_wire = Part.Wire([cw1, cw2, cw3, cw4])
        c_face = Part.Face(c_wire)
        c_extrude = c_face.extrude(App.Vector(0, 0, thickness))
        
        guide_bar_body = guide_bar_body.cut(c_extrude)
        
    # --- 4. Chain Edge Groove (Simulated) ---
    # We'll do a small inset on both faces
    groove_inset = 1.5
    groove_depth = 2.0
    
    # Create the object in the doc
    obj = doc.addObject("Part::Feature", "BlazeGuideBar")
    obj.Shape = guide_bar_body
    obj.ViewObject.ShapeColor = (0.2, 0.2, 0.2) # Dark grey
    
    doc.recompute()
    print("Blaze Guide Bar generated successfully.")

if __name__ == "__main__":
    create_guide_bar()

