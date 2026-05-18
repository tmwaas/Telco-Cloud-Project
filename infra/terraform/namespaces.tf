resource "kubernetes_namespace" "ran" {
  metadata {
    name = "ns-ran"
  }
}

resource "kubernetes_namespace" "core" {
  metadata {
    name = "ns-core"
  }
}

resource "kubernetes_namespace" "platform" {
  metadata {
    name = "ns-platform"
  }
}
