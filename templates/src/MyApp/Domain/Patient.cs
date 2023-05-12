using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace E.ApplicationCore.Domain
{
    public class Patient
    {
        public string Email { get; set; }
        public string CIN { get; set; }
        public DateTime DateNaissance { get; set; }


    }
}
