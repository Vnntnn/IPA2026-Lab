locals {
  # A single naming prefix used everywhere
  name_prefix = "${var.project_name}-${var.environment}"
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

  # Derived boolean - production gets stricter settings
  is_production = var.environment == "prod"
}
