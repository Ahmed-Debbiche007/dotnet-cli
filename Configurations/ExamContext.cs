using E.ApplicationCore.Domain;
using E.Infrastructure.Configurations;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace E.Infrastructure
{
    public class ExamenContext:DbContext
    {
		public DbSet<Adm> Adms { get; set; }
		public DbSet<Clinique> Cliniques { get; set; }
		public DbSet<Chambre> Chambres { get; set; }
		public DbSet<Patient> Patients { get; set; }
		public DbSet<Admission> Admissions { get; set; }
        //Add DBsets Here

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseLazyLoadingProxies();
            optionsBuilder.UseSqlServer(@"Data Source=(localdb)\mssqllocaldb;
                       Initial Catalog=DABNomPrenom3;
                       Integrated Security=true;MultipleActiveResultSets=true");

            base.OnConfiguring(optionsBuilder);
        
    }
        //application de fluent API
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
				modelBuilder.ApplyConfiguration(new ChambreConfiguration() );
				modelBuilder.ApplyConfiguration(new AdmissionConfiguration() );
				modelBuilder.ApplyConfiguration(new AdmissionConfiguration() );
				modelBuilder.ApplyConfiguration(new AdmissionConfiguration() );
				modelBuilder.ApplyConfiguration(new AdmissionConfiguration() );
//config
        }
        // appliquer une condition sur les prop de type string
        protected override void ConfigureConventions(ModelConfigurationBuilder configurationBuilder)
        {
            configurationBuilder.Properties<string>().HaveMaxLength(50);
        }
    }
}
