from path_builder import PathBuilder


top_folder

output = convert_ccfx_output(self.pb,proj,lang, is_new)
rep_out_path = self.pb.getRepertoireOutputPath(lang, is_new)
suffix = '_old.txt'
if is_new:
    suffix = '_new.txt'
output.writeToFile(rep_out_path + lang + suffix)
self.progress('Repertoire filtering based on operation')
