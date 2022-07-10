   ManagementObjectSearcher objSearcher = new ManagementObjectSearcher(
           "SELECT * FROM Win32_SoundDevice");

    ManagementObjectCollection objCollection = objSearcher.Get();

    foreach (ManagementObject obj in objCollection)
    {
        foreach (PropertyData property in obj.Properties)
        {
            Console.Out.WriteLine(String.Format("{0}:{1}", property.Name, property.Value));
        }
    }

    