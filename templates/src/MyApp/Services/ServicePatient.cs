using E.ApplicationCore.Domain;
using E.ApplicationCore.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace E.ApplicationCore.Services
{
    public class ServicePatient : Service<Patient>, IServicePatient
    {
        public ServicePatient(IUnitOfWork unitOfWork) : base(unitOfWork)
        {
        }

       
    }
}
