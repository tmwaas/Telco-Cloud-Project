resource "kubernetes_service_account" "deploy_sa" {
  metadata {
    name      = "deploy-automation"
    namespace = "ns-platform"
  }
}

resource "kubernetes_role" "deploy_role" {
  metadata {
    name      = "deploy-role"
    namespace = "ns-platform"
  }

  rule {
    api_groups = [""]
    resources  = ["pods", "services", "endpoints", "configmaps"]
    verbs      = ["get", "list", "watch", "create", "update", "delete"]
  }
}

resource "kubernetes_role_binding" "deploy_binding" {
  metadata {
    name      = "deploy-binding"
    namespace = "ns-platform"
  }

  role_ref {
    kind      = "Role"
    name      = kubernetes_role.deploy_role.metadata[0].name
    api_group = "rbac.authorization.k8s.io"
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.deploy_sa.metadata[0].name
    namespace = "ns-platform"
  }
}
