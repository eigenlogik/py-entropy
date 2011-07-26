# Entropy Scripting Wrapper

py-entropy is a Python wrapper around [Entropy's](http://www.entropyapp.com/) AppleScript layer. You can use it to perform tasks such as:

- Creating archives ( including encrypted and multi-volume archives )
- Extracting archives
- Inspecting the contents of an archive

## Requirements

You will need Entropy ( v1.3+ ) and [AppScript for Python](http://appscript.sourceforge.net/).

## Notes

The `archive` and `unarchive` commands are asynchronous. That is, they return immediately after the archiving/extraction has begun, without waiting for completion.

## Further information

[The Entropy Scripting Guide](http://www.entropyapp.com/scripting)

## License

py-entropy is licensed under the MIT license : http://www.opensource.org/licenses/mit-license.php