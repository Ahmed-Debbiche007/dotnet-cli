using E.ApplicationCore.Interfaces;
using E.ApplicationCore.Services;
using E.Infrastructure;
using E.Interfaces;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);


// Injection de d�pendance
builder.Services.AddDbContext<DbContext, ExamContext>();
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddSingleton<Type>(t => typeof(GenericRepository<>));

//*******************
builder.Services.AddScoped<IServiceClinique, ServiceClinique>();
builder.Services.AddScoped<IServiceChambre, ServiceChambre>();
builder.Services.AddScoped<IServicePatient, ServicePatient>();
builder.Services.AddScoped<IServiceAdmission, ServiceAdmission>();
//builder_services
//................



// Add services to the container.
builder.Services.AddControllersWithViews();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();