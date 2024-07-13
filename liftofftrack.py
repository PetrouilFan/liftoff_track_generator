import xml.etree.ElementTree as ET
from xml.dom import minidom

class Object:
    def __init__(self, itemID, instanceID, position, rotation):
        self.itemID = itemID
        self.instanceID = instanceID
        self.position = position
        self.rotation = rotation
    
    def export(self):
        track = ET.Element("TrackBlueprint")
        track.set("xsi:type", "TrackBlueprintFlag")
        itemID = ET.SubElement(track, "itemID")
        itemID.text = str(self.itemID)
        instanceID = ET.SubElement(track, "instanceID")
        instanceID.text = str(self.instanceID)
        position = ET.SubElement(track, "position")
        x = ET.SubElement(position, "x")
        x.text = str(self.position[0])
        y = ET.SubElement(position, "y")
        y.text = str(self.position[1])
        z = ET.SubElement(position, "z")
        z.text = str(self.position[2])
        rotation = ET.SubElement(track, "rotation")
        x = ET.SubElement(rotation, "x")
        x.text = str(self.rotation[0])
        y = ET.SubElement(rotation, "y")
        y.text = str(self.rotation[1])
        z = ET.SubElement(rotation, "z")
        z.text = str(self.rotation[2])
        return track

class SpawnPoint(Object):
    def __init__(self, instanceID, position, rotation):
        super().__init__("SpawnPointSingle02", instanceID, position, rotation)

class Cube05x05(Object):
    def __init__(self, instanceID, position, rotation):
        super().__init__("DrawingBoardCube0.5mx0.5m01", instanceID, position, rotation)

class DrawingBoardWall5mx5m(Object):
    def __init__(self, instanceID, position, rotation):
        super().__init__("DrawingBoardWall5mx5m01", instanceID, position, rotation)

class DrawingBoardWall5mx5m(Object):
    def __init__(self, instanceID, position, rotation):
        super().__init__("DrawingBoardCube1mx1m01", instanceID, position, rotation)

class Track:
    def __init__(self, track_name, game_version, localID):
        self.track_name = track_name
        self.game_version = game_version
        self.localID = localID
        self.objects = []

    def _export(self):
        root = ET.Element("Track")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        gameVersion = ET.SubElement(root, "gameVersion")
        gameVersion.text = self.game_version
        localID = ET.SubElement(root, "localID")
        str = ET.SubElement(localID, "str")
        #TODO: FIX THIS
        str.text = self.localID
        version = ET.SubElement(localID, "version")
        version.text = "1"
        type = ET.SubElement(localID, "type")
        type.text = "TRACK"
        name = ET.SubElement(root, "name")
        name.text = self.track_name
        description = ET.SubElement(root, "description")
        description.text = ""
        dependencies = ET.SubElement(root, "dependencies")
        environment = ET.SubElement(root, "environment")
        environment.text = "TheDrawingBoard"
        blueprints = ET.SubElement(root, "blueprints")
        for obj in self.objects:
            blueprints.append(obj.export()) 
        return root
    
    def export_file(self, filename):
        root = self._export()
        Track._write_xml(root, filename)

    @staticmethod
    def _write_xml(root, filename):
        tree = ET.ElementTree(root)
        xml_str = ET.tostring(tree.getroot(), encoding="UTF-8", xml_declaration=True)
        parsed_str = minidom.parseString(xml_str)
        pretty_xml_str = parsed_str.toprettyxml(indent="  ", encoding="utf-8").decode('utf-8')
        with open(filename, "w") as file:
            file.write(pretty_xml_str)

    def add_spawn_point(self, position, rotation):
        spawn_point = SpawnPoint(len(self.objects), position, rotation)
        self.objects.append(spawn_point)