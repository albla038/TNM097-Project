import { ImageIcon, X } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadItem,
  FileUploadItemDelete,
  FileUploadItemMetadata,
  FileUploadItemPreview,
  FileUploadList,
  FileUploadTrigger,
} from "@/components/ui/file-upload";
import { useCallback, useState } from "react";

export function ImageUploadDropZone() {
  const [files, setFiles] = useState<File[]>([]);

  const onFileReject = useCallback((file: File, message: string) => {
    toast.error(message, {
      description: `"${file.name}" was rejected`,
    });
  }, []);

  return (
    <FileUpload
      accept="image/*"
      maxFiles={1}
      maxSize={8 * 1024 * 1024}
      className="w-full max-w-md"
      value={files}
      onValueChange={setFiles}
      onFileReject={onFileReject}
      multiple={false}
    >
      <FileUploadDropzone className="border-primary/20 bg-primary/5 hover:bg-primary/10 data-dragging:bg-primary/10">
        <div className="flex flex-col items-center gap-2 text-center">
          <div className="rounded-lg bg-primary/10 p-3">
            <ImageIcon className="size-8 text-primary" />
          </div>
          <div>
            <p className="text-sm font-medium">Upload image</p>
            <p className="text-xs text-muted-foreground">
              PNG, JPG, WEBP, BMP or TIFF up to 8MB
            </p>
          </div>
        </div>
        <FileUploadTrigger asChild>
          <Button size="sm" className="mt-3">
            Select Image
          </Button>
        </FileUploadTrigger>
      </FileUploadDropzone>
      <FileUploadList>
        {files.map((file, index) => (
          <FileUploadItem key={index} value={file}>
            <FileUploadItemPreview />
            <FileUploadItemMetadata />
            <FileUploadItemDelete asChild>
              <Button variant="ghost" size="icon" className="size-7">
                <X className="size-4" />
              </Button>
            </FileUploadItemDelete>
          </FileUploadItem>
        ))}
      </FileUploadList>
    </FileUpload>
  );
}

