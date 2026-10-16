data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_security_group" "web" {
  name        = "${var.name_prefix}-web-sg"
  description = "Dynamically generated ingress rules"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      description = ingress.value.description
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.name_prefix}-web-sg" })
}

resource "aws_instance" "server" {
  for_each = var.servers

  ami = data.aws_ami.amazon_linux.id

  # Per-server size, taken from the map
  instance_type = each.value.instance_type

  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.web.id]
  associate_public_ip_address = true

  root_block_device {
    volume_size = var.root_volume.size_gb
    volume_type = var.root_volume.type
    encrypted   = var.root_volume.encrypted
  }

  user_data = <<-EOF
    #!/bin/bash
    dnf install -y nginx
    echo "<h1>Hello from Terraform - $(hostname)</h1>" > /usr/share/nginx/html/index.html
    systemctl enable --now nginx
  EOF

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-${each.key}"
    Role = each.value.role
  })
}
