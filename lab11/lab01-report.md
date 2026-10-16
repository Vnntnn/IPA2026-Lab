# Questions
### Question 1: Why is pinning the provider version important for a team project? Write your answer in your lab report.
**Ans** Because it's make team working same terraform version environment, reduce syntax occurs when using different terraform cli version

### Question 2: How many resources will be added?
**Ans** 2 resources adding are instance and security group

### Question 3: Which attributes show as (known after apply), and why can Terraform not know them yet?
**Ans** 
```bash
# aws_instance.web will be created
  + resource "aws_instance" "web" {
      + ami                                  = "ami-0b2c9d1f3edcfd709"
      + arn                                  = (known after apply)
      + associate_public_ip_address          = (known after apply)
      + availability_zone                    = (known after apply)
      + cpu_core_count                       = (known after apply)
      + cpu_threads_per_core                 = (known after apply)
      + disable_api_stop                     = (known after apply)
      + disable_api_termination              = (known after apply)
      + ebs_optimized                        = (known after apply)
      + enable_primary_ipv6                  = (known after apply)
      + get_password_data                    = false
      + host_id                              = (known after apply)
      + host_resource_group_arn              = (known after apply)
      + iam_instance_profile                 = (known after apply)
      + id                                   = (known after apply)
      + instance_initiated_shutdown_behavior = (known after apply)
      + instance_lifecycle                   = (known after apply)
      + instance_state                       = (known after apply)
      + instance_type                        = "t3.micro"
      + ipv6_address_count                   = (known after apply)
      + ipv6_addresses                       = (known after apply)
      + key_name                             = (known after apply)
      + monitoring                           = (known after apply)
      + outpost_arn                          = (known after apply)
      + password_data                        = (known after apply)
      + placement_group                      = (known after apply)
      + placement_partition_number           = (known after apply)
      + primary_network_interface_id         = (known after apply)
      + private_dns                          = (known after apply)
      + private_ip                           = (known after apply)
      + public_dns                           = (known after apply)
      + public_ip                            = (known after apply)
      + secondary_private_ips                = (known after apply)
      + security_groups                      = (known after apply)
      + source_dest_check                    = true
      + spot_instance_request_id             = (known after apply)
      + subnet_id                            = (known after apply)
      + tags                                 = {
          + "Name" = "lab01-web-server"
        }
      + tags_all                             = {
          + "Course"    = "IPA-Terraform"
          + "ManagedBy" = "Terraform"
          + "Name"      = "lab01-web-server"
        }
      + tenancy                              = (known after apply)
      + user_data                            = "7d0b62e8e8f9c59ed25f055f3f470acc91accece"
      + user_data_base64                     = (known after apply)
      + user_data_replace_on_change          = false
      + vpc_security_group_ids               = (known after apply)

      + capacity_reservation_specification (known after apply)

      + cpu_options (known after apply)

      + ebs_block_device (known after apply)

      + enclave_options (known after apply)

      + ephemeral_block_device (known after apply)

      + instance_market_options (known after apply)

      + maintenance_options (known after apply)

      + metadata_options (known after apply)

      + network_interface (known after apply)

      + private_dns_name_options (known after apply)

      + root_block_device (known after apply)
    }

  # aws_security_group.web will be created
  + resource "aws_security_group" "web" {
      + arn                    = (known after apply)
      + description            = "Allow HTTP inbound and all outbound"
      + egress                 = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 0
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "-1"
              + security_groups  = []
              + self             = false
              + to_port          = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + id                     = (known after apply)
      + ingress                = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "HTTP from anywhere"
              + from_port        = 80
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 80
            },
        ]
      + name                   = "lab01-web-sg"
      + name_prefix            = (known after apply)
      + owner_id               = (known after apply)
      + revoke_rules_on_delete = false
      + tags                   = {
          + "Name" = "lab01-web-sg"
        }
      + tags_all               = {
          + "Course"    = "IPA-Terraform"
          + "ManagedBy" = "Terraform"
          + "Name"      = "lab01-web-sg"
        }
      + vpc_id                 = "vpc-0888952142de383b3"
    }
```

### Question 4: Does Terraform plan to update in place or to replace the instance? Look for the ~ or -/+ symbol and explain what it means.
**Ans**
```bash
Terraform will perform the following actions:

  # aws_instance.web will be updated in-place
  ~ resource "aws_instance" "web" {
        id                                   = "i-0bba425d59b6e9bb4"
      ~ instance_type                        = "t3.micro" -> "t3.small"
      ~ public_dns                           = "ec2-32-199-165-247.compute-1.amazonaws.com" -> (known after apply)
      ~ public_ip                            = "32.199.165.247" -> (known after apply)
        tags                                 = {
            "Name" = "lab01-web-server"
        }
        # (37 unchanged attributes hidden)

        # (8 unchanged blocks hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

### Question 5: How did the plan output change compared to Step 4.1? Why would this matter for a production web server?
**Ans**
```bash
Terraform will perform the following actions:

  # aws_instance.web will be updated in-place
  ~ resource "aws_instance" "web" {
        id                                   = "i-0bba425d59b6e9bb4"
      ~ instance_type                        = "t3.micro" -> "t3.small"
      ~ public_dns                           = "ec2-32-199-165-247.compute-1.amazonaws.com" -> (known after apply)
      ~ public_ip                            = "32.199.165.247" -> (known after apply)
        tags                                 = {
            "Name" = "lab01-web-server"
        }
        # (37 unchanged attributes hidden)

        # (8 unchanged blocks hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

### Question 6: What error do you get, and at what stage does it occur — plan or apply?
**Ans**
```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform planned the following actions, but then encountered a problem:

  # aws_instance.web will be destroyed
  - resource "aws_instance" "web" {
      - ami                                  = "ami-0b2c9d1f3edcfd709" -> null
      - arn                                  = "arn:aws:ec2:us-east-1:059006792171:instance/i-0bba425d59b6e9bb4" -> null
      - associate_public_ip_address          = true -> null
      - availability_zone                    = "us-east-1d" -> null
      - cpu_core_count                       = 1 -> null
      - cpu_threads_per_core                 = 2 -> null
      - disable_api_stop                     = false -> null
      - disable_api_termination              = false -> null
      - ebs_optimized                        = false -> null
      - get_password_data                    = false -> null
      - hibernation                          = false -> null
      - id                                   = "i-0bba425d59b6e9bb4" -> null
      - instance_initiated_shutdown_behavior = "stop" -> null
      - instance_state                       = "running" -> null
      - instance_type                        = "t3.micro" -> null
      - ipv6_address_count                   = 0 -> null
      - ipv6_addresses                       = [] -> null
      - monitoring                           = false -> null
      - placement_partition_number           = 0 -> null
      - primary_network_interface_id         = "eni-0efcb548bb831158f" -> null
      - private_dns                          = "ip-172-31-19-104.ec2.internal" -> null
      - private_ip                           = "172.31.19.104" -> null
      - public_dns                           = "ec2-32-199-165-247.compute-1.amazonaws.com" -> null
      - public_ip                            = "32.199.165.247" -> null
      - secondary_private_ips                = [] -> null
      - security_groups                      = [
          - "lab01-web-sg",
        ] -> null
      - source_dest_check                    = true -> null
      - subnet_id                            = "subnet-03494ccf5a4b740f7" -> null
      - tags                                 = {
          - "Name" = "lab01-web-server"
        } -> null
      - tags_all                             = {
          - "Course"    = "IPA-Terraform"
          - "ManagedBy" = "Terraform"
          - "Name"      = "lab01-web-server"
        } -> null
      - tenancy                              = "default" -> null
      - user_data                            = "7d0b62e8e8f9c59ed25f055f3f470acc91accece" -> null
      - user_data_replace_on_change          = false -> null
      - vpc_security_group_ids               = [
          - "sg-0bc0985f43c570778",
        ] -> null
        # (8 unchanged attributes hidden)

      - capacity_reservation_specification {
          - capacity_reservation_preference = "open" -> null
        }

      - cpu_options {
          - core_count       = 1 -> null
          - threads_per_core = 2 -> null
            # (1 unchanged attribute hidden)
        }

      - credit_specification {
          - cpu_credits = "unlimited" -> null
        }

      - enclave_options {
          - enabled = false -> null
        }

      - maintenance_options {
          - auto_recovery = "default" -> null
        }

      - metadata_options {
          - http_endpoint               = "enabled" -> null
          - http_protocol_ipv6          = "disabled" -> null
          - http_put_response_hop_limit = 2 -> null
          - http_tokens                 = "required" -> null
          - instance_metadata_tags      = "disabled" -> null
        }

      - private_dns_name_options {
          - enable_resource_name_dns_a_record    = false -> null
          - enable_resource_name_dns_aaaa_record = false -> null
          - hostname_type                        = "ip-name" -> null
        }

      - root_block_device {
          - delete_on_termination = true -> null
          - device_name           = "/dev/xvda" -> null
          - encrypted             = false -> null
          - iops                  = 3000 -> null
          - tags                  = {
              - "Course"    = "IPA-Terraform"
              - "ManagedBy" = "Terraform"
            } -> null
          - tags_all              = {
              - "Course"    = "IPA-Terraform"
              - "ManagedBy" = "Terraform"
            } -> null
          - throughput            = 125 -> null
          - volume_id             = "vol-07fc9bcc909385a05" -> null
          - volume_size           = 8 -> null
          - volume_type           = "gp3" -> null
            # (1 unchanged attribute hidden)
        }
    }

Plan: 0 to add, 0 to change, 1 to destroy.
╷
│ Error: Instance cannot be destroyed
│ 
│   on main.tf line 42:
│   42: resource "aws_instance" "web" {
│ 
│ Resource aws_instance.web has lifecycle.prevent_destroy set, but the plan calls for this resource to be destroyed. To avoid this error and continue with the plan, either disable
│ lifecycle.prevent_destroy or reduce the scope of the plan using the -target option.
```
