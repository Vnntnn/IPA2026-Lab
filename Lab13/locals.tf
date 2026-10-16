locals {
  # A single naming prefix used everywhere
  name_prefix = "${var.project_name}-${var.environment}"

  # Ternary: production gets a bigger instance
  effective_instance_type = local.is_production ? "t3.medium" : var.instance_type

  # Production gets a larger, encrypted root volume
  effective_volume_size = local.is_production ? 30 : var.root_volume.size_gb

  # Only open SSH to the office CIDR outside production
  ssh_cidrs = local.is_production ? [] : ["10.0.0.0/8"]

  # Tags merged from a fixed set plus whatever the caller supplies
  common_tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "IPA-Student"
    },
    var.extra_tags
  )

  # Root volume assembled from the ternary above. Production is always encrypted.
  effective_root_volume = {
    size_gb   = local.effective_volume_size
    type      = var.root_volume.type
    encrypted = local.is_production ? true : var.root_volume.encrypted
  }

  # Derived boolean - production gets stricter settings
  is_production = var.environment == "prod"

  # for + merge over a map of objects. In production every server is forced up
  # to local.effective_instance_type; otherwise each server keeps its own size.
  effective_servers = {
    for name, cfg in var.servers : name => merge(cfg, {
      instance_type = local.is_production ? local.effective_instance_type : cfg.instance_type
    })
  }

  candidate_ingress = [
    {
      description = "HTTP"
      port        = 80
      protocol    = "tcp"
      cidr_blocks = var.allowed_http_cidrs
    },
    {
      description = "Application port added by the caller"
      port        = 8080
      protocol    = "tcp"
      cidr_blocks = var.allowed_http_cidrs
    },
    {
      description = "SSH from the office network"
      port        = 22
      protocol    = "tcp"
      cidr_blocks = local.ssh_cidrs
    },
  ]

  # for ... if drops any rule with an empty CIDR list. local.ssh_cidrs is []
  # in production, so the SSH rule simply disappears there.
  ingress_rules = [
    for rule in local.candidate_ingress : rule
    if length(rule.cidr_blocks) > 0
  ]
}
