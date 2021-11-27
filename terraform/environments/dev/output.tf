output "lb_dns" {
  value = module.load_balancer.dns_name
}

output "domain" {
  value = module.dns.domain
}