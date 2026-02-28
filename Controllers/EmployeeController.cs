using Microsoft.AspNetCore.Mvc; 
using System.Text.Json; 
using System.Collections.Generic; 
using System.IO; 
namespace EmployeeRestApi.Controllers 
{ 
    [ApiController] 
    [Route("api/[controller]")] 
    public class EmployeeController : ControllerBase 
    { 
        [HttpGet] 
        public IActionResult Get() 
        { 
            return Ok(employees); 
        } 
    } 
} 
