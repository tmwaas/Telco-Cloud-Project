data "aws_availability_zones" "az" {}
resource "aws_vpc" "this" {
  cidr_block = "10.50.0.0/16"
  tags = {
    Name = "telco-eks"
  }
}
resource "aws_subnet" "public_a" {
  vpc_id = aws_vpc.this.id
  cidr_block = "10.50.1.0/24"
  availability_zone = data.aws_availability_zones.az.names[0]
  map_public_ip_on_launch = true
  tags = { 
    Name = "public-a" 
  }
}
resource "aws_subnet" "public_b" {
  vpc_id = aws_vpc.this.id
  cidr_block = "10.50.2.0/24"
  availability_zone = data.aws_availability_zones.az.names[1]
  map_public_ip_on_launch = true
  tags = {
    Name = "public-b"
  }
}
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.this.id 
}
resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.this.id 
  route {
    cidr_block = "0.0.0.0/0" 
    gateway_id = aws_internet_gateway.igw.id 
  }
}
resource "aws_route_table_association" "rta" {
  subnet_id = aws_subnet.public_a.id 
  route_table_id = aws_route_table.rt.id 
}
