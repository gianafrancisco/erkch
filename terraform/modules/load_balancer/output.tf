output "dns_name" {
  value = aws_lb.lb.dns_name
}

output "target_groups" {
  value = aws_lb_target_group.tg
}