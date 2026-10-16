### Checkpoint 1: Record the output of every expression above in your report.

```text
> 5 + 3 * 2
11
> 10 % 3
1
> "a" == "a" && 1 < 2
true
> 3 > 5 ? "big" : "small"
"small"
> var.environment == "prod" ? "t3.large" : "t3.micro"
"t3.micro"
> upper("terraform")
"TERRAFORM"
> join("-", ["ipa", "lab03", "web"])
"ipa-lab03-web"
> split(",", "a,b,c")
tolist([
  "a",
  "b",
  "c",
])
> format("%s-%03d", "web", 7)
"web-007"
> substr("hello world", 0, 5)
"hello"
> trimspace(" padded ")
"padded"
> replace("my_project_name", "_", "-")
"my-project-name"
> length(["a", "b", "c"])
3
> merge({a = 1}, {b = 2})
{
  "a" = 1
  "b" = 2
}
> keys({name = "kmitl", age = 60})
[
  "age",
  "name",
]
> values({name = "kmitl", age = 60})
[
  60,
  "kmitl",
]
> lookup({a = 1, b = 2}, "c", "default")
"default"
> contains(["dev", "prod"], "dev")
true
> toset(["a", "b", "a"])
toset([
  "a",
  "b",
])
> flatten([[1, 2], [3, 4]])
[
  1,
  2,
  3,
  4,
]
> zipmap(["a", "b"], [1, 2])
{
  "a" = 1
  "b" = 2
}
> regex("[0-9]+", "instance-42-web")
"42"
> regexall("[a-z]+", "ab12cd34ef")
tolist([
  "ab",
  "cd",
  "ef",
])
> can(regex("^t[23]\\.", "t3.micro"))
true
> can(regex("^t[23]\\.", "m5.large"))
false
> tostring(42)
"42"
> tonumber("3.14")
3.14
> tolist(toset(["b", "a"]))
tolist([
  "a",
  "b",
])
> try(tonumber("not-a-number"), 0)
0
> can(tonumber("not-a-number"))
false
```

---

### Question 1: What is the difference between try() and can()? When would you reach for each?

**<u>Answer:</u>** 
`try()` เอาไว้หาค่าสำรองเวลาข้อมูลหายหรือพัง ทำ fallback เพื่อให้โค้ดรันต่อได้ไม่ล่ม เหมาะกับการดึงค่า optional หรือ JSON ที่ไม่แน่นอน เช่น try(local.raw.timeout, 30)

ส่วน `can()` เอาไว้เช็คว่าโค้ดรันผ่านไหม โดยคืนค่าเป็น true หรือ false เหมาะกับการเอาไปใส่ในบล็อก validation เพื่อตรวจสอบความถูกต้องของตัวแปรที่รับเข้ามา

---

### Checkpoint 2: Show both results side by side in your report.

| Expression | dev (default) | `-var="environment=prod"` |
|---|---|---|
| `local.effective_instance_type` | `"t3.micro"` | `"t3.medium"` |
| `local.is_production` | `false` | `true` |

---

### Question 2: Which instance does Terraform destroy? Now imagine you had 3 instances and wanted to remove the middle one. What would count do? This is the classic count pitfall.

**<u>Answer:</u>** 
พอลด `instance_count` จาก 2 เป็น 1 Terraform จะลบตัวท้ายสุดคือ `aws_instance.web[1]` ส่วน `web[0]` อยู่เหมือนเดิม เพราะ count ใช้แค่ตัวเลข index เรียงจาก 0 ขึ้นไป พอจำนวนลดมันก็ตัดจากท้ายก่อนเสมอ

ถ้ามี 3 ตัวแล้วอยากเอาตัวกลาง (`web[1]`) ออก count ทำให้ไม่ได้ครับ ลดเหลือ 2 ก็ได้ลบ `web[2]` อยู่ดี ตัวที่เราอยากเอาออกยังค้างอยู่ ที่แย่กว่านั้นคือถ้า resource สร้างมาจาก list แล้วเราลบของกลางออกจาก list ตัวที่อยู่หลังจะเลื่อน index ขึ้นมา Terraform ก็จะเห็นว่า `web[1]` มี config เปลี่ยนไป (ต้อง update หรือสร้างใหม่) แล้วค่อยไปลบ `web[2]` ทิ้ง ทั้งที่เราแค่ลบไปตัวเดียว นี่แหละคือ count pitfall

---

### Checkpoint 3: Compare the resource addresses: aws_instance.web[0] versus aws_instance.server["web"].

**<u>Answer:</u>** 
ตอนใช้ count address จะเป็นเลข index (`aws_instance.web[0]`, `web[1]`) พอเปลี่ยนเป็น for_each address กลายเป็น key ที่เราตั้งเอง ตัวนี้เป็นของจริงจาก `terraform state list` หลัง apply:

```text
module.web_server.aws_instance.server["api"]
module.web_server.aws_instance.server["web"]
```

แล้วลองเอา `api` ออกจาก map ผล plan ได้แบบนี้ (ตัว `web` ไม่ถูกแตะเลย):

```text
  # module.web_server.aws_instance.server["api"] will be destroyed
  # (because key ["api"] is not in for_each map)
Plan: 0 to add, 0 to change, 1 to destroy.
```

หลัง apply ลอง curl ทั้งสองเครื่อง nginx ขึ้นปกติ ได้หน้า `Hello from Terraform - ip-10-0-1-120.ec2.internal` (api) กับ `... ip-10-0-1-191.ec2.internal` (web)

---

### Question 3: Removing api from the for_each map destroys only the api instance. Explain in one sentence why for_each is safer than count for non-identical resources.

**<u>Answer:</u>** 
เพราะ for_each จำ resource แต่ละตัวด้วย key ที่ตั้งเอง (เช่น `server["api"]`) ไม่ได้จำด้วยลำดับ พอลบ key ไหน Terraform ก็ลบแค่ตัวนั้น ตัวอื่นที่ config ไม่เหมือนกันไม่โดนเลื่อนหรือสร้างใหม่ตามไปด้วย

---

### Question 4: Rewrite [for k, v in var.servers : k if v.role == "backend"] using only functions (keys, lookup, etc.). Which version is more readable?

**<u>Answer:</u>** 
ลองใน console แล้ว ใช้ `matchkeys` ได้:

```hcl
matchkeys(keys(var.servers), values(var.servers)[*].role, ["backend"])
```

ผลได้ `tolist(["api"])` ตรงกับ for expression เดิม

แต่ว่าแบบ `for ... if` อ่านง่ายกว่าเยอะ อ่านแล้วเข้าใจทันทีว่า "เอา key ที่ role เป็น backend" ส่วน matchkeys ต้องมานั่งดูว่า argument แต่ละตัวคืออะไร แล้วยังต้องเชื่อว่า `keys()` กับ `values()` เรียงลำดับตรงกัน และเช็คได้แค่ว่า "เท่ากับค่าที่ระบุ" ถ้าเงื่อนไขซับซ้อนกว่านี้ก็ใช้ไม่ได้

---

### Checkpoint 4: Show the plan diff proving the third ingress rule appeared.

**<u>Answer:</u>** 
ผลจาก `terraform plan` (dev) ใน `aws_security_group.web` ได้ ingress 3 rule คือ 80, 8080 และ 22 โดยไม่ได้แตะไฟล์ module เลย:

```text
      + ingress                = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "Application port added by the caller"
              + from_port        = 8080
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 8080
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "HTTP"
              + from_port        = 80
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 80
            },
          + {
              + cidr_blocks      = [
                  + "10.0.0.0/8",
                ]
              + description      = "SSH from the office network"
              + from_port        = 22
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 22
            },
        ]
```

---

### Checkpoint 5: Show the dev and prod plans side by side and point out all three differences.

**<u>Answer:</u>** 

| | `terraform plan` (dev) | `terraform plan -var="environment=prod"` |
|---|---|---|
| ingress ports | 80, 8080, 22 | 80, 8080 |
| instance_type (ทั้ง 2 ตัว) | t3.micro | t3.medium |
| root volume_size | 8 GB | 30 GB |
| root volume encrypted | true | true |

สามอย่างที่เปลี่ยนไป ซึ่งมาจาก ternary ที่เขียนไว้ใน Part 2:
1. rule SSH (port 22) หายไป เพราะ `ssh_cidrs` เป็น `[]` แล้ว `for ... if length(rule.cidr_blocks) > 0` กรองทิ้ง
2. instance ทั้งสองตัวจาก `t3.micro` กลายเป็น `t3.medium`
3. root volume จาก 8 GB เป็น 30 GB (encrypted เป็น true ทั้งคู่ เพราะ default ของ dev ก็เปิดอยู่แล้ว แต่ prod ถูกบังคับให้เปิดเสมอ)

---

### Question 5: In the dynamic "ingress" block, what do ingress.key and ingress.value refer to? What would they be if for_each were a map instead of a list?

**<u>Answer:</u>** 
ชื่อ iterator ใน `dynamic` จะเป็นชื่อเดียวกับ label ของ block คือ `ingress` ถ้า `for_each` เป็น list `ingress.key` คือ index ของสมาชิก (0, 1, 2) ส่วน `ingress.value` คือสมาชิกตัวนั้นทั้งก้อน ซึ่งในแล็บนี้เป็น object ของ rule เลยเรียกใช้เป็น `ingress.value.port`, `ingress.value.cidr_blocks` ได้

ถ้า `for_each` เป็น map แทน `ingress.key` จะเป็น key ของ map (เป็น string) และ `ingress.value` เป็นค่าที่คู่กับ key นั้น

---

### Part 6: Clean Up

รัน destroy เสร็จแล้ว ได้ `Apply complete! Resources: 0 added, 0 changed, 14 destroyed.` และ `terraform state list` ว่างเปล่า (0 รายการ)
