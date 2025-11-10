def copyFilesToLocal(srcPath, dstPath):
    print(srcPath)
    newFiles = 0
    existingFiles = 0
    errFiles = 0
    if "CT_LogArchive" in srcPath:  # New logfile drive
        zipFiles = glob.glob(os.path.join(srcPath, r"*_SiDaNet_Logfiles_*.zip"))
        zipFiles.sort()
        for z in zipFiles:
            try:
                if os.path.getsize(z) == 0:
                    continue
                metaPath = os.path.join(dstPath, "meta")
                inputPath = os.path.join(dstPath, "input")
                os.makedirs(metaPath, exist_ok=True)
                os.makedirs(inputPath, exist_ok=True)
                with zipfile.ZipFile(z, "r") as f:
                    files = f.namelist()
                    if len(files) > 0:
                        if not os.path.isdir(dstPath):
                            os.mkdir(dstPath)
                            os.makedirs(metaPath, exist_ok=True)
                            os.makedirs(inputPath, exist_ok=True)
                        for file in files:
                            if file.endswith(".log"):
                                outDir = inputPath
                            else:
                                outDir = os.path.join(dstPath, "other")
                                os.makedirs(outDir, exist_ok=True)
                            outFileName = os.path.basename(z) + "__" + file
                            outFilePath = os.path.join(outDir, outFileName)
                            if os.path.isfile(outFilePath):
                                existingFiles += 1
                            else:
                                with open(outFilePath, "wb") as w:
                                    w.write(f.read(file))
                                info = f.getinfo(file)
                                srcmtime = calendar.timegm(info.date_time)  # original 6-tuple
                                os.utime(outFilePath, (srcmtime, srcmtime))
                                newFiles += 1
            except:
                print("Error with zip file")
                print(z)
                traceback.print_exc(file=sys.stdout)
                errFiles += 1
    return newFiles, existingFiles, errFiles
