### Question 1: After you apply, what does Terraform print where a sensitive value would appear? Is the value still stored in the state file? (Answer from the book, Chapter 3.3.)

**<u>Answer:</u>** 
Terraform output ไม่แสดงข้อมูลที่ทำการตั้งค่า sensitive เอาไว้ จะซ่อนข้อมูลทั้งตอนระหว่าง plan และ apply แต่ยังมีการเก็บข้อมูลที่ sensitive เป็น plain text ไว้ที่ terraform state file

---
### Question 2: What is the difference between a local and a variable with a default? Give one situation where only a local will work.

**<u>Answer:</u>** 
ความต่างหลัก ๆ คือ เรื่องการแก้ค่าจากข้างนอก ตัว variable ที่ใส่ default ไว้ ต่อให้มีค่าเริ่มต้นมาให้ คนที่เอาโมดูลไปใช้ก็ยังส่งค่าใหม่มาทับได้อยู่ดี แต่ถ้าเป็น local จะเหมือนตัวแปรส่วนตัวที่ใช้แค่ข้างในโมดูล คนข้างนอกจะมาแตะต้องหรือเปลี่ยนค่ามันไม่ได้เลย

เคสที่ต้องใช้ local แน่ๆ คือเวลาเราอยากคำนวณค่าจากตัวแปรอื่น เช่น เอาชื่อโปรเจกต์กับ environment มาต่อสตริงกันเพื่อทำ prefix ตั้งชื่อ resource แบบนี้ variable ทำไม่ได้ เพราะค่า default ของมันบังคับให้ใส่เป็นค่าคงที่นิ่งๆ ห้ามอ้างอิงตัวแปรอื่น เลยต้องโยนมาคิดใน local แทน

---
### Question 3: Terraform will likely plan to destroy and recreate your resources even though the configuration is functionally identical. Why?

**<u>Answer:</u>** 
พอเราย้าย resource จาก root module ไปไว้ใน child module (เช่น `module.web_server`) ตัว resource address มันจะเปลี่ยนตามไปด้วย (จาก `aws_instance.web` กลายเป็น `module.web_server.aws_instance.web`)

ทีนี้ Terraform มันจำ resource ต่างๆ ผ่านทาง address ในไฟล์ state ครับ พอ address ใหม่มันยังไม่มีอยู่ใน state ตัว Terraform เลยคิดว่าต้องสร้าง resource ขึ้นมาใหม่ และพอหา address เดิมในโค้ดไม่เจอแล้ว มันก็เลยจะสั่งลบ resource ตัวเก่าทิ้ง

---
### Question 4: Why is ```version = "~> 5.0"``` required for a registry module but not for a local ```./modules/...``` module?

**<u>Answer:</u>** 
Registry module จะเป็นการดึงโค้ดมาจากภายนอก ซึ่งเจ้าของอาจมีการอัปเดตโค้ดใหม่ได้ตลอดเวลา เราเลยต้องล็อคเวอร์ชันเอาไว้เพื่อให้แน่ใจว่าใช้เวอร์ชันที่เข้ากันได้ และกันไม่ให้ระบบพังถ้าเขาปล่อยเวอร์ชันใหม่ออกมา ส่วน local module ไฟล์มันจะอยู่ในเครื่องเราเองและไปพร้อมกับโค้ดหลักเลย เราจึงคุมโค้ดได้โดยตรง จึงไม่ต้องมีระบบล็อคเวอร์ชันแยกเหมือนกับตัวที่โหลดมาจากข้างนอก

---
### What did moving code into a module make easier, and what did it make harder?

การย้ายโค้ดไปเป็น modules ช่วยให้เรานำ infrastructure เดิมกลับมาใช้ซ้ำในโปรเจกต์หรือ environment อื่นๆ ได้ง่ายขึ้น แถมยังช่วยให้โค้ดหลักดูสะอาดตาขึ้นเพราะมันซ่อนรายละเอียดข้างในไว้ แต่ข้อเสียคือช่วงแรกจะ setup ยากขึ้นหน่อย เพราะเราต้องมาคอยกำหนด interface ทั้งตัวแปร input และ outputs เพื่อส่งข้อมูล input output ตัว modules อย่างชัดเจน ยิ่งถ้าเป็นการย้าย resource ที่มีอยู่แล้วเข้า modules เรายิ่งต้องระวังเรื่องการย้าย state (เช่น ต้องเขียน moved block) ไม่อย่างนั้น Terraform จะเผลอไปลบของเดิมแล้วสร้างใหม่ให้แทน

---