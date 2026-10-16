data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "web" {
  name        = "lab01-web-sg"
  description = "Allow HTTP inbound and all outbound"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "lab01-web-sg"
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web.id]
  user_data              = <<-EOF
#!/bin/bash
dnf install -y nginx
echo "<h1>Hello from Terraform - $(hostname)</h1>" > /usr/share/nginx/html/ind
ex.html
systemctl enable --now nginx
EOF
  tags = {
    Name = "lab01-web-server"
  }
  lifecycle {
    // prevent_destroy = true
  }
}