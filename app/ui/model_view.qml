import QtQuick 2.15
import QtQuick3D

Item {
    width: 600
    height: 360

    View3D {
        anchors.fill: parent
        environment: SceneEnvironment {
            backgroundMode: SceneEnvironment.Color
            clearColor: "#050505"
        }

        PerspectiveCamera {
            id: camera
            position: Qt.vector3d(0, 0, 600)
            lookAtNode: modelNode
        }

        DirectionalLight {
            eulerRotation.x: -35
            eulerRotation.y: 30
            brightness: 1.25
        }

        Node {
            id: modelNode
            scale: Qt.vector3d(100, 100, 100)

            SceneLoader {
                id: loader
                source: modelUrl
            }
        }
    }

    PropertyAnimation {
        target: modelNode
        property: "eulerRotation.y"
        from: 0
        to: 360
        duration: 12000
        loops: Animation.Infinite
        running: true
    }

    MouseArea {
        anchors.fill: parent
        enabled: false
    }
}